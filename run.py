#!/usr/bin/env python3

import sys
from agents import build_agents

def main():
    if len(sys.argv) < 2:
        print(
            """
            Usage: python run.py \"<your travel request>\"\n
            Examples:
                "Please help me plan a trip from Salt Lake City to New York City from 01/10/26 to 01/20/26"
                "I would like to go on a week long trip from Denver to Paris leaving on February 17th. My budget is $3500."
                "What are some travel options next week to Chicago from SLC?"
            """
        )
        return
    query = sys.argv[1]
    researcher, planner = build_agents(verbose=2)
    print("Query:", query)
    research_data = researcher.run(query)
    
    planning_prompt = f"User Request: {query}\n\nResearch Data Provided:\n{research_data}"
    result = planner.run(planning_prompt)
    
    print("\n=== Final Answer ===\n", result)

if __name__ == "__main__":
    main()
