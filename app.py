from flask import Flask, request
import psycopg2
import pandas as pd

app = Flask(__name__)

def etl():
    # Load CSV files and clean the dataframe
    # load users.csv file
    users_df = pd.read_csv("./data/users.csv")
    users_df.columns = users_df.columns.str.replace("\t", "")
    users_df[["name", "email", "signup_date"]] = users_df[["name", "email", "signup_date"]].apply(lambda x: x.str.replace("\t",""))
    
    # load user_experiments.csv file
    user_experiments_df = pd.read_csv("data/user_experiments.csv")
    user_experiments_df.columns = user_experiments_df.columns.str.replace("\t", "")
    user_experiments_df["experiment_compound_ids"] = user_experiments_df["experiment_compound_ids"].str.replace('\t', '')
    
    # load compounds.csv file and remove unnecessary "\t"
    compounds_df = pd.read_csv("data/compounds.csv")
    compounds_df.columns = compounds_df.columns.str.replace("\t", "")
    compounds_df[["compound_name", "compound_structure"]] = compounds_df[["compound_name", "compound_structure"]].apply(lambda x: x.str.replace('\t', ''))

    # Process files to derive features
    # caluculate total experiments for each user
    total_experiments = user_experiments_df.groupby('user_id').size().reset_index(name='total_experiments')
    
    # calculate average experiments per user
    average_experiments = user_experiments_df.groupby('user_id').size().mean()

    # calcurate user's most commonly experimented compound
    compound_counts = user_experiments_df['experiment_compound_ids'].str.split(';').explode().value_counts()
    most_common_compound = compounds_df[compounds_df['compound_id'] == int(compound_counts.idxmax())]

    # Upload processed data into a database
    
    # Connect to Postgres database
    conn = psycopg2.connect(
        host='postgres',
        port=5432,
        dbname='test_database',
        user='test_user',
        password='test_password'
    )
    cur = conn.cursor()
    
    # create database table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_features (
            user_id INTEGER PRIMARY KEY,
            total_experiments INTEGER,
            average_experiments FLOAT,
            most_common_compound_id INTEGER,
            most_common_compound_name VARCHAR(255),
            most_common_compound_structure VARCHAR(255)
        )
    ''')

    # Insert the derived features into the database
    for index, row in total_experiments.iterrows():
        user_id = row['user_id']
        experiments = row['total_experiments']
        average = average_experiments
        compound_id = most_common_compound['compound_id'].values[0]
        compound_name = most_common_compound['compound_name'].values[0]
        compound_structure = most_common_compound['compound_structure'].values[0]

        # Convert numpy.int64 values to native Python integers
        user_id = int(user_id)
        experiments = int(experiments)
        average = float(average)
        compound_id = int(compound_id)
        

        cur.execute('''
            INSERT INTO user_features (
                user_id,
                total_experiments,
                average_experiments,
                most_common_compound_id,
                most_common_compound_name,
                most_common_compound_structure
            ) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (user_id, experiments, average, compound_id, compound_name, compound_structure))

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()
    
    
    
# Your API that can be called to trigger your ETL process
def trigger_etl():
    # Trigger your ETL process here
    etl()
    return {"message": "ETL process started"}, 200


def show_user_features():
    # Connect to Postgres database
    conn = psycopg2.connect(
        host='postgres',
        port=5432,
        dbname='test_database',
        user='test_user',
        password='test_password'
    )
    cur = conn.cursor()
    
    # Check if the user_features table exists
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user_features')")
    table_exists = cur.fetchone()[0]

    if table_exists:
        cur.execute('SELECT * FROM user_features')
        rows = cur.fetchall()
    else:
        rows = []

    cur.close()
    conn.close()
    
    return rows

@app.route('/')
def index():
    return 'This is an ETL application'

@app.route('/etl', methods=['POST'])
def etl_route():
    return trigger_etl()

@app.route('/database', methods=['POST'])
def database_route():
    rows = show_user_features()
    return {'user_features': rows}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)