import React from 'react';
import PropTypes from 'prop-types';

import User from 'components/User';

const UsersList = ({ users, toggleUser }) => {
    const usersList = users.map(user => 
          <tr key={user.twitter_id}>
              <td className={user.selected ? 'bg-primary' : ''}>
                  <a onClick={(event) => toggleUser(user, event)}>
                      <User user={user} toggleUser={toggleUser}/>
                    </a>
                </td>
            </tr>
    );
    return (
        <table className="table table-sm table-hover">
            <thead>
                <tr>
                    <th>Users</th>
                </tr>
            </thead>
            <tbody>
                {usersList}
            </tbody>
        </table>
    );
};

UsersList.propTypes = {
    users: PropTypes.array.isRequired,
    toggleUser: PropTypes.func.isRequired,
};

export default UsersList;
