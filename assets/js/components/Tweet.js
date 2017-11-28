import React from 'react';
import PropTypes from 'prop-types';

const Tweet = ({ twitter_id, text, user, created_at }) => {

  return (
      <li>
        <strong>{text}</strong> <small>{created_at}</small>
      </li>
  );
};

Tweet.propTypes = {
  twitter_id: PropTypes.number.isRequired,
  text: PropTypes.string.isRequired,
  user: PropTypes.number.isRequired,
  created_at: PropTypes.string.isRequired,
};

export default Tweet;
