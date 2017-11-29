import React from 'react';
import UsersList from 'components/UsersList';


export default class UsersListContainer extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      users: []
    };
  }

  componentDidMount() {
    this.setState({
       users: [
          {
            twitter_id: 1,
            screen_name: 'twitterUser',
            name: 'User',
            description: 'Twitter User'
          },
          {
            twitter_id: 2,
            screen_name: 'coolUser',
            name: 'Cool User',
            description: 'Cool User'
          }
        ]
    })
  }

  addUser(user) {
      this.state.users.push(user);
  }

  render() {
    return <UsersList users={this.state.users} />;
  }
}
