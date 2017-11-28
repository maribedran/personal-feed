import React from 'react';
import PropTypes from 'prop-types';

const User = ({ twitter_id, screen_name, description }) => {

  return (
      <li>
        <strong>@{screen_name}</strong>
      </li>
  );
};

User.propTypes = {
  twitter_id: PropTypes.number.isRequired,
  screen_name: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
};

export default User;
