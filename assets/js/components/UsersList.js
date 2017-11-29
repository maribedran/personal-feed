import React from 'react';
import PropTypes from 'prop-types';

import User from 'components/User';

const UsersList = ({ users, selectUserCallback }) => {

    return (
        <table className="table table-sm table-hover">
            <thead>
                <tr>
                    <th>Users</th>
                </tr>
            </thead>
            <tbody>
                {users.map((user) =>
                    <User key={user.twitter_id} user={user} selectUser={selectUserCallback}/>
                )}
            </tbody>
        </table>
    );
};

UsersList.propTypes = {
    users: PropTypes.array.isRequired,
};

export default UsersList;
