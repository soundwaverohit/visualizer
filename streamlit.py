import streamlit as st
import json

st.title("JSON Problem Visualizer and Editor")

# Create tabs
tab1, tab2 = st.tabs(["Visualize JSON", "Edit JSON"])

# Shared variable for JSON content
if 'json_content' not in st.session_state:
    st.session_state.json_content = None

with tab1:
    st.header("Visualize JSON")

    st.markdown("### Paste your JSON content below and click Submit:")
    with st.form(key='visualize_form'):
        json_input_visualize = st.text_area("JSON Input", height=300)
        submit_button_visualize = st.form_submit_button(label='Submit')

    if submit_button_visualize:
        if json_input_visualize:
            try:
                json_content = json.loads(json_input_visualize)
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
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please paste the JSON content before submitting.")

with tab2:
    st.header("Edit JSON")

    st.markdown("### Paste your JSON content below and click Submit:")
    with st.form(key='edit_form'):
        json_input_edit = st.text_area("JSON Input", height=300)
        submit_button_edit = st.form_submit_button(label='Submit')

    if submit_button_edit:
        if json_input_edit:
            try:
                st.session_state.json_content = json.loads(json_input_edit)
                st.success("JSON content loaded successfully.")
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {e}")
                st.session_state.json_content = None
        else:
            st.warning("Please paste the JSON content before submitting.")
            st.session_state.json_content = None

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

            create_json_button = st.form_submit_button(label="Create JSON file")

            if create_json_button:
                try:
                    # Convert the updated data back to JSON
                    new_json_content = json.dumps(updated_json, indent=4)
                    st.success("Updated JSON content:")
                    st.code(new_json_content, language='json')
                except Exception as e:
                    st.error(f"Error creating JSON: {e}")
