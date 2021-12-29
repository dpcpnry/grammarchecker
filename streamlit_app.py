'''Check spelling and basic grammar.

Use gingerit, a wrapper around gingersoftware.com API
See https://github.com/Azd325/gingerit

@pnry 28 Dec 2021
'''

import streamlit as st
from gingerit.gingerit import GingerIt

Parser = GingerIt()
show_definition = False


def ginger_check(text, show_defi=False):
    try:
        results = Parser.parse(text.strip())
        if results:
            show_results(text, results, show_defi)
    except Exception as e:
        st.error(e)


def show_results(text, results, show_defi):
    n = 0
    edits = ''
    text_u = text
    text_correct = text
    if not results:
        st.write('No results to show!')
        return
    for info in reversed(results['corrections']):
        if info:
            if info['text'] and info['correct']:
                text_u = text_u.replace(
                    info['text'], '<span class="uword">' + info['text'] + '</span>', 1)
                text_correct = text_correct.replace(
                    info['text'], '**`' + info['correct'] + '`**', 1)

                n = n + 1
                if info['definition'] and show_defi:
                    edits += f"{n}. **{info['text']}** -> **{info['correct']}** : {info['definition']}\n"
                else:
                    edits += f"{n}. **{info['text']}** -> **{info['correct']}**\n"
    if n > 0:
        st.markdown(
            '''<style>.uword {border-bottom: solid orange 2pt;}</style>''',
            unsafe_allow_html=True)

        # col_left, col_right = st.columns(2)

        # shown as columns in mobile browsers
        # with col_left:
        st.warning(f'⚠️ Potential issues: {n}')
        st.markdown(text_u, unsafe_allow_html=True)

        # with col_right:
        st.success(f'💡 Suggested corrections: {n}')
        st.markdown(text_correct)

        st.warning(f'Modifications: {n}')
        st.markdown(edits)

        st.write('')

        st.success('### Final Result')
        st.write(results['result'])

    else:
        st.write('No Suggested Corrections')

    # st.markdown('### JSON output')
    # st.json(results)


# ---------- streamlit ----------
# When a user interacts with widgets in the app:
# Streamlit will rerun the code from top to bottom
# ---------- streamlit ----------
st.set_page_config(
    page_title='Basic Grammar checker',
    page_icon='📝',
    layout='wide',
)

st.markdown('## 📑 Basic Grammar Checker')

form = st.form(key='grammar_checker')

text = form.text_area(
    label='Enter text',
    placeholder='Enter a sentence or a short paragraph',
    help='Powered by gingerit and gingersoftware.com')

show_definition = st.checkbox('Show definition')

submit = form.form_submit_button(label='Check')

if submit:
    if text:
        # with st.spinner('Checking...'):
        ginger_check(text, show_definition)
    else:
        st.write('Enter a sentence!')
