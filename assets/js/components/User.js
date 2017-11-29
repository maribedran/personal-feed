import React from 'react';
import PropTypes from 'prop-types';

const User = ({ user, selectUser }) => {

    return (
        <tr>
            <td>
                <input type="checkbox"
                       value={user.selected}
                       onChange={(event) => selectUser(user, event)}/>
                <strong> {user.name}</strong> @{user.screen_name}
            </td>
        </tr>
    );
};

User.propTypes = {
    user: PropTypes.object.isRequired,
    selectUser: PropTypes.func.isRequired,
};

export default User;
