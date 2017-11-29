import React from 'react';
import PropTypes from 'prop-types';

import Tweet from 'components/Tweet';

const TweetsList = ({ tweets }) => {

    return (
        <div className="row">
            {tweets.map((tweet) =>
            <Tweet
                key={tweet.twitter_id.toString()}
                twitter_id={tweet.twitter_id}
                text={tweet.text}
                user={tweet.user}
                created_at={tweet.created_at}/>
            )}
        </div>
    );
};

TweetsList.propTypes = {
    tweets: PropTypes.array.isRequired,
};

export default TweetsList;
