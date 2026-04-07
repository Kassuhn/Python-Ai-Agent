import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("api key is set to none")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="User input parser")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(model = "gemini-2.5-flash"
,     contents = messages, config = types.GenerateContentConfig(tools=[available_functions],
                                                                 system_instruction=system_prompt,
                                                                   temperature=0))
    
    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")
    
    function_responses = []

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens:  {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call=function_call, verbose=args.verbose)
                
                if not function_call_result.parts or not function_call_result.parts[0].function_response or not function_call_result.parts[0].function_response.response:
                    raise RuntimeError(f"Empty or invalid function response for: {function_call.name}")
            
                print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
        else:
            print(response.text)
    else:
        if response.function_calls:
            for function_call in response.function_calls:

                function_call_result = call_function(function_call=function_call)
                
                if not function_call_result.parts or not function_call_result.parts[0].function_response or not function_call_result.parts[0].function_response.response:
                    raise RuntimeError(f"Empty or invalid function response for: {function_call.name}")
            
                function_responses.append(function_call_result.parts[0])

        else:
            print(response.text)



if __name__ == "__main__":
    main()
