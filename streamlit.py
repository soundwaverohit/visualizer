import streamlit as st
import json
import requests
from urllib.parse import urlparse
from base64 import b64encode

st.title("GitHub JSON Problem Visualizer and Editor")

# Create tabs
tab1, tab2 = st.tabs(["Visualize JSON", "Edit JSON"])

# Shared variable for JSON content
if 'json_content' not in st.session_state:
    st.session_state.json_content = None
if 'github_repo_url' not in st.session_state:
    st.session_state.github_repo_url = ''
if 'github_pat' not in st.session_state:
    st.session_state.github_pat = ''

def get_raw_github_content_link(github_link):
    # Convert GitHub URL to raw content URL
    if "github.com" in github_link:
        github_link = github_link.replace("github.com", "raw.githubusercontent.com")
        github_link = github_link.replace("/blob/", "/")
    return github_link

def get_github_api_url(github_link):
    # Convert GitHub URL to API URL
    parsed_url = urlparse(github_link)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) >= 4 and path_parts[2] == 'blob':
        owner = path_parts[0]
        repo = path_parts[1]
        branch = path_parts[3]
        file_path = '/'.join(path_parts[4:])
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        return api_url, owner, repo, branch, file_path
    else:
        return None, None, None, None, None

with tab1:
    st.header("Visualize JSON")

    st.markdown("### Enter the GitHub URL of the JSON file and click Submit:")
    with st.form(key='visualize_form'):
        github_url = st.text_input("GitHub URL", value=st.session_state.github_repo_url)
        submit_button_visualize = st.form_submit_button(label='Submit')

    if submit_button_visualize:
        if github_url:
            st.session_state.github_repo_url = github_url
            raw_url = get_raw_github_content_link(github_url)
            try:
                response = requests.get(raw_url)
                if response.status_code == 200:
                    json_content = response.json()
                    st.session_state.json_content = json_content
                    st.success("JSON content loaded successfully.")

                    # Display Problem Name
                    st.header(json_content.get("problem_name", "Problem"))
                    # Display Problem Description
                    problem_description_main = json_content.get("problem_description_main", "")
                    if problem_description_main:
                        st.markdown("### Problem Description")
                        st.markdown(problem_description_main)
                    # Display Problem Background
                    problem_background_main = json_content.get("problem_background_main", "")
                    if problem_background_main:
                        st.markdown("### Background")
                        st.markdown(problem_background_main)
                    # Display Input/Output
                    problem_io = json_content.get("problem_io", "")
                    if problem_io:
                        st.markdown("### Input/Output")
                        st.code(problem_io, language='python')
                    # Display Required Dependencies
                    required_dependencies = json_content.get("required_dependencies", "")
                    if required_dependencies:
                        st.markdown("### Required Dependencies")
                        st.code(required_dependencies, language='python')
                    # Display Sub-Steps
                    sub_steps = json_content.get("sub_steps", [])
                    for step in sub_steps:
                        st.subheader(f"Step {step.get('step_number', '')}")
                        step_description = step.get("step_description_prompt", "")
                        if step_description:
                            st.markdown("#### Description")
                            st.markdown(step_description)
                        step_background = step.get("step_background", "")
                        if step_background:
                            st.markdown("#### Background")
                            st.markdown(step_background)
                        function_header = step.get("function_header", "")
                        if function_header:
                            st.markdown("#### Function Header")
                            st.code(function_header, language='python')
                        ground_truth_code = step.get("ground_truth_code", "")
                        if ground_truth_code:
                            st.markdown("#### Solution Code")
                            st.code(ground_truth_code, language='python')
                        return_line = step.get("return_line", "")
                        if return_line:
                            st.markdown("#### Return Line")
                            st.code(return_line, language='python')
                        test_cases = step.get("test_cases", [])
                        if test_cases:
                            st.markdown("#### Test Cases")
                            for test in test_cases:
                                st.code(test, language='python')
                    # Display General Solution
                    general_solution = json_content.get("general_solution", "")
                    if general_solution:
                        st.header("General Solution")
                        st.code(general_solution, language='python')
                    # Display General Tests
                    general_tests = json_content.get("general_tests", [])
                    if general_tests:
                        st.header("General Tests")
                        for test in general_tests:
                            st.code(test, language='python')
                else:
                    st.error(f"Failed to fetch JSON file. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter the GitHub URL before submitting.")

with tab2:
    st.header("Edit JSON")

    if st.session_state.json_content:
        st.markdown("---")
        st.subheader("Editable Fields")

        with st.form(key='edit_fields_form'):
            updated_json = st.session_state.json_content.copy()

            # Editable fields for problem_description_main, problem_background_main, problem_io
            updated_json['problem_description_main'] = st.text_area(
                "Problem Description Main",
                value=updated_json.get('problem_description_main', ''),
                height=150
            )

            updated_json['problem_background_main'] = st.text_area(
                "Problem Background Main",
                value=updated_json.get('problem_background_main', ''),
                height=150
            )

            updated_json['problem_io'] = st.text_area(
                "Problem I/O",
                value=updated_json.get('problem_io', ''),
                height=150
            )

            # Editable fields for sub_steps
            sub_steps = updated_json.get('sub_steps', [])
            updated_sub_steps = []

            for idx, step in enumerate(sub_steps):
                st.markdown(f"#### Sub-Step {idx + 1}: Step {step.get('step_number', '')}")
                step_copy = step.copy()
                step_copy['step_description_prompt'] = st.text_area(
                    f"Step Description Prompt (Step {step.get('step_number', '')})",
                    value=step.get('step_description_prompt', ''),
                    height=100,
                    key=f'step_description_prompt_{idx}'
                )
                step_copy['step_background'] = st.text_area(
                    f"Step Background (Step {step.get('step_number', '')})",
                    value=step.get('step_background', ''),
                    height=100,
                    key=f'step_background_{idx}'
                )
                step_copy['function_header'] = st.text_area(
                    f"Function Header (Step {step.get('step_number', '')})",
                    value=step.get('function_header', ''),
                    height=100,
                    key=f'function_header_{idx}'
                )
                step_copy['ground_truth_code'] = st.text_area(
                    f"Ground Truth Code (Step {step.get('step_number', '')})",
                    value=step.get('ground_truth_code', ''),
                    height=200,
                    key=f'ground_truth_code_{idx}'
                )
                step_copy['return_line'] = st.text_area(
                    f"Return Line (Step {step.get('step_number', '')})",
                    value=step.get('return_line', ''),
                    height=70,
                    key=f'return_line_{idx}'
                )
                # Test cases as list of strings
                test_cases = step.get('test_cases', [])
                test_cases_str = '\n'.join(test_cases)
                test_cases_input = st.text_area(
                    f"Test Cases (one per line) (Step {step.get('step_number', '')})",
                    value=test_cases_str,
                    height=150,
                    key=f'test_cases_{idx}'
                )
                step_copy['test_cases'] = test_cases_input.strip().split('\n') if test_cases_input.strip() else []
                updated_sub_steps.append(step_copy)
                st.markdown("---")

            updated_json['sub_steps'] = updated_sub_steps

            # GitHub Personal Access Token input
            st.markdown("### GitHub Authentication")
            st.warning("To push changes to GitHub, you need to provide a GitHub Personal Access Token (PAT) with 'repo' scope permissions. Do not share this token with anyone.")
            github_pat = st.text_input("GitHub Personal Access Token (PAT)", type="password")
            st.session_state.github_pat = github_pat

            create_json_button = st.form_submit_button(label="Create JSON file and Push to GitHub")

            if create_json_button:
                if not github_pat:
                    st.error("Please provide your GitHub Personal Access Token.")
                else:
                    try:
                        # Convert the updated data back to JSON
                        new_json_content = json.dumps(updated_json, indent=4)

                        # Push the new JSON file to GitHub
                        api_url, owner, repo, branch, file_path = get_github_api_url(st.session_state.github_repo_url)
                        if api_url and owner and repo and branch and file_path:
                            # Set the new file path to 'modified.json' in the same directory
                            modified_file_path = '/'.join(file_path.split('/')[:-1] + ['modified.json'])
                            api_put_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{modified_file_path}"

                            # Get the SHA of the existing file if it exists
                            headers = {
                                "Authorization": f"token {github_pat}",
                                "Accept": "application/vnd.github.v3+json"
                            }
                            get_response = requests.get(api_put_url + f"?ref={branch}", headers=headers)
                            if get_response.status_code == 200:
                                sha = get_response.json()['sha']
                            else:
                                sha = None  # File doesn't exist; will be created

                            # Prepare the data for the PUT request
                            data = {
                                "message": "Update modified.json via Streamlit app",
                                "content": b64encode(new_json_content.encode('utf-8')).decode('utf-8'),
                                "branch": branch
                            }
                            if sha:
                                data["sha"] = sha

                            put_response = requests.put(api_put_url, headers=headers, data=json.dumps(data))

                            if put_response.status_code in [200, 201]:
                                st.success(f"modified.json has been successfully updated in the repository.")
                                file_url = f"https://github.com/{owner}/{repo}/blob/{branch}/{modified_file_path}"
                                st.markdown(f"[View modified.json in GitHub]({file_url})")
                            else:
                                st.error(f"Failed to update modified.json. Status code: {put_response.status_code}")
                                st.error(put_response.json())
                        else:
                            st.error("Invalid GitHub URL. Please ensure it points to a file in a repository.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
    else:
        st.warning("Please load and submit a JSON file in the Visualize JSON tab before editing.")
