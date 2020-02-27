import os
import json
import pickle
from glob import glob

root_path = "/".join(os.path.abspath(__file__).split("/")[:-2])
sessions_path = os.path.join(root_path, "sessions")


def create_session():
    """Creates a new experiment or session

    Returns:
        Whether this session was succefully created
    """

    if not os.path.exists(sessions_path):
        os.mkdir(sessions_path)

    session_id = __get_next_session_id__()
    print(session_id)
    session_path = os.path.join(sessions_path, session_id)

    if os.path.exists(session_path):
        return None
    else:
        # Create directory
        os.mkdir(session_path)

        # Create new boost instance
        # state = create_state()
        state = {}

        # Save new state
        save_state(session_id, state)

        return session_id


def delete_session(session_id):
    """Deletes session

    Args:
        session_id: ID of given session

    Returns:
        Whether this session was succefully created
    """

    session_path = os.path.join(sessions_path, session_id)

    if not os.path.exists(session_path):
        return False
    else:
        # Remove directory
        os.remove(session_path)

        return True


def load_state(session_id):
    """Loads a session state

    Args:
        session_id: Session ID

    Returns:
        State is returned
    """
    state_folder = os.path.join(sessions_path, session_id)

    if os.path.exists(state_folder):
        with open(os.path.join(state_folder, "state.pkl"), "rb") as f:
            return pickle.load(f)

    else:
        return None


def save_state(session_id, state):
    """Takes in a state and saves it to the session

    Args:
        session_id: Session ID
        state: State to save.

    Returns:
        Bool is return for if this succeeded or not
    """

    state_folder = os.path.join(sessions_path, session_id)

    if os.path.exists(state_folder):
        with open(os.path.join(state_folder, "state.pkl"), "wb") as f:
            pickle.dump(state, f)

        return True
    else:
        return False


def __get_next_session_id__():
    """Finds the next unused session id

    Returns:
        integer of the next session id
    """
    session_paths = glob(os.path.join(sessions_path, "*"))

    # If there are no sessions, start the ids at 0
    if len(session_paths) == 0:
        return str(0)

    session_numbers = [int(path.split("/")[-1]) for path in session_paths]
    return str(sorted(session_numbers)[-1] + 1)