import React from 'react';
import PropTypes from 'prop-types';

import Tweet from 'components/Tweet';

const TweetsList = ({ tweets }) => {

  return (
      <div>
          <h2>All tweets</h2>
          <ul>
              {tweets.map((tweet) =>
                <Tweet
                    key={tweet.twitter_id.toString()}
                    twitter_id={tweet.twitter_id}
                    text={tweet.text}
                    user={tweet.user}
                    created_at={tweet.created_at}/>
              )}
          </ul>
      </div>
  );
};

TweetsList.propTypes = {
  tweets: PropTypes.array.isRequired,
};

export default TweetsList;
