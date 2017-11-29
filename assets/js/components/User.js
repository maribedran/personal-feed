import React from 'react';
import PropTypes from 'prop-types';

const User = ({ twitter_id, screen_name, name, description }) => {

  return (
      <tr>
        <td><strong>{name}</strong> @{screen_name}</td>
      </tr>
  );
};

User.propTypes = {
  twitter_id: PropTypes.number.isRequired,
  screen_name: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
};

export default User;
