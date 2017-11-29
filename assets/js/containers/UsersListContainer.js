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
                    description: 'Twitter User',
                    selected: false
                },
                {
                    twitter_id: 2,
                    screen_name: 'coolUser',
                    name: 'Cool User',
                    description: 'Cool User',
                    selected: false
                }
            ]
        })
    }

    selectUser(user, event) {
        user.selected = event.target.checked;
        console.log(user);
        console.log(event);
    }

    addUser(user) {
        this.state.users.push(user);
    }

    render() {
        return <UsersList users={this.state.users} selectUserCallback={this.selectUser} />;
    }
}
