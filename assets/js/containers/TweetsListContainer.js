import React from 'react';
import TweetsList from 'components/TweetsList';


export default class TweetsListContainer extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      tweets: []
    };
  }

  componentDidMount() {
    this.setState({
       tweets: [
         {
           twitter_id: 1,
           text: 'My Tweet',
           user: {
             twitter_id: 1,
             screen_name: 'twitterUser',
             name: 'User',
             description: 'Twitter User'
           },
           created_at: '2017-01-01 10:00:00'
         },
         {
           twitter_id: 2,
           text: 'My Awesome Tweet',
           user: {
             twitter_id: 2,
             screen_name: 'coolUser',
             name: 'Cool User',
             description: 'Cool User'
           },
           created_at: '2017-01-02 11:00:00'
         }
       ]
    })
  }

  addTweet(tweet) {
      this.state.tweets.push(tweet);
  }

  render() {
    return <TweetsList tweets={this.state.tweets} />;
  }
}
