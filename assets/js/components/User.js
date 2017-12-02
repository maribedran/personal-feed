import React from 'react';
import PropTypes from 'prop-types';

const User = ({ user }) => {
    return (
        <div><strong> {user.name}</strong> @{user.screen_name}</div>
    );
};

User.propTypes = {
    user: PropTypes.object.isRequired,
};

export default User;
