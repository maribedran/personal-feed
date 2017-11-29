import React from 'react';
import PropTypes from 'prop-types';

const Tweet = ({ twitter_id, text, user, created_at }) => {

  return (
      <div className="card col-sm-12">
  		<div className="card-block">
        	<p><strong>{user.name}</strong> @{user.screen_name} <small>{created_at}</small></p>
        	<p>{text}</p>
      	</div>
      </div>
  );
};

Tweet.propTypes = {
  twitter_id: PropTypes.number.isRequired,
  text: PropTypes.string.isRequired,
  user: PropTypes.object.isRequired,
  created_at: PropTypes.string.isRequired,
};

export default Tweet;
