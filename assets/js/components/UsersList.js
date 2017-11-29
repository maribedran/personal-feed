import React from 'react';
import PropTypes from 'prop-types';

import User from 'components/User';

const UsersList = ({ users }) => {

  return (
    <table className="table table-sm table-hover">
      <thead>
        <tr>
          <th>Users</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user) =>
          <User
              key={user.twitter_id.toString()}
              twitter_id={user.twitter_id}
              screen_name={user.screen_name}
              name={user.name}
              description={user.description}/>
        )}
      </tbody>
    </table>
  );
};

UsersList.propTypes = {
  users: PropTypes.array.isRequired,
};

export default UsersList;
