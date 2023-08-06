import os
import textwrap


def update_prompt():
    # TODO: maybe we should create a bashrc, if there is none?
    _update_bashrc() or _update_bash_profile()
    _update_zshrc()


def _update_bashrc():
    return _update_rc_file(os.path.expanduser('~/.bashrc'),
                           _create_bash_prompt())


def _update_bash_profile():
    return _update_rc_file(os.path.expanduser('~/.bash_profile'),
                           _create_bash_prompt())


def _create_bash_prompt():
    return textwrap.dedent(r'''
        if [ -n "$VIRTUAL_ENV_NAME" ]; then
            export PS1="\[[0;33m\](${VIRTUAL_ENV_NAME})\[[0m\]$PS1"
        elif [ -n "$VIRTUAL_ENV" ]; then
            export PS1="\[[0;33m\](${VIRTUAL_ENV##*/})\[[0m\]$PS1"
        fi
    ''').strip()


def _update_zshrc():
    prompt = textwrap.dedent(r'''
        if [ -n "$VIRTUAL_ENV_NAME" ]; then
            export PROMPT="%{[0;33m%}(${VIRTUAL_ENV_NAME})%{[0m%}$PROMPT"
        elif [ -n "$VIRTUAL_ENV" ]; then
            export PROMPT="%{[0;33m%}(${VIRTUAL_ENV##*/})%{[0m%}$PROMPT"
        fi
    ''').strip()
    return _update_rc_file(os.path.expanduser('~/.zshrc'), prompt)


def _update_rc_file(rcfile, prompt):
    try:
        content = open(rcfile).read()
    except FileNotFoundError:
        return False
    # skip the update if there is something similar
    if 'VIRTUAL_ENV_NAME' in content:
        return True
    code = '\n'
    if content[-1] != '\n':
        code += '\n'
    code += textwrap.dedent(r'''
        # The next block was inserted by the `projects' module of
        # The SCORE Framework (http://score-framework.org)

            # This next line updates your shell prompt to include the name of
            # the current project.
    ''').lstrip()
    code += textwrap.indent(prompt, '    ') + '\n'
    open(rcfile, 'a').write(code)
    return True
