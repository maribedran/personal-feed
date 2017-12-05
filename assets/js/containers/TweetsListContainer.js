import React from 'react';
import axios from 'axios';

import TweetsList from 'components/TweetsList';


export default class TweetsListContainer extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      tweets: []
    };
  }

  fetchTweets() {
    axios.get('/api/twitter/tweets/')
    .then((response) => {
      this.setState({tweets: response.data.results});
    })
    .catch((error) => {
      console.log(error);
    });
  }

  componentDidMount() {
    this.fetchTweets();
  }

  render() {
    return <TweetsList tweets={this.state.tweets} />;
  }
}
