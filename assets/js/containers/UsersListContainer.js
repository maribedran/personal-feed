import React from 'react';
import axios from 'axios';

import UsersList from 'components/UsersList';


export default class UsersListContainer extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            users: []
        };
    }

    fetchUsers() {
        axios.get('/api/twitter/users/')
            .then((response) => {
                let users = response.data.results.map((user) => {
                    user.selected = false;
                    return user;
                  });
                  this.setState({users});
            })
            .catch((error) => {
                console.log(error);
            });
    }

    componentDidMount() {
        this.fetchUsers();
    }

    toggleUser(user, event) {
        user.selected = !user.selected;
        this.setState(this.state);
    }

    addUser(user) {
        this.state.users.push(user);
    }

    render() {
        return <UsersList users={this.state.users} toggleUser={this.toggleUser.bind(this)} />;
    }
}
