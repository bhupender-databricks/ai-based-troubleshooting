from langchain.agents import create_csv_agent
from langchain.agents.agent_types import AgentType
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import csv
import re
import streamlit as st


def convert_log_to_csv_and_store(dir_path, csv_file_prefix, csv_dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.log'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    with open(os.path.join(csv_dir_path, csv_file_prefix + '_' + file.split('.')[0] + '.csv'), 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        for line in lines:
                            line = line.strip()
                            if line:
                                line = re.sub(',', '","', line)
                                line = '"' + line + '"'
                                writer.writerow([line])

def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="AI based Troubleshooting platform")
    st.header("AI based Troubleshooting platform")

    # filenames = []
    # for root,dirs, files in os.walk('./csv'):
    #     for file in files:
    #         if file.endswith('csv'):
    #             filenames.append(os.path.join(root, file))
    # print(filenames)

    csv_file = ['./csv/main_Apache_2k.csv', './csv/main_HPC_2k.csv', './csv/main_BGL_2k.csv', './csv/main_SSH_2k.csv', './csv/main_Mac_2k.csv']

    if csv_file is not None:

        agent = create_csv_agent(
            OpenAI(temperature=0),
            csv_file,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            max_execution_time=100,
            early_stopping_method="generate",
        )

        user_question = st.text_input("Ask a question to your troubleshooting bot:")

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                st.write(agent.run(user_question))


if __name__ == "__main__":
    dir_path = './loghub'
    csv_file_prefix = 'main'
    csv_dir_path = './csv'
    convert_log_to_csv_and_store(dir_path, csv_file_prefix, csv_dir_path)
    main()
