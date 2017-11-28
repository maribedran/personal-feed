import React from 'react';
import PropTypes from 'prop-types';

import User from 'components/User';

const UsersList = ({ users }) => {

  return (
      <div>
          <h2>All users</h2>
          <ul>
              {users.map((user) =>
                <User
                    key={user.twitter_id.toString()}
                    twitter_id={user.twitter_id}
                    screen_name={user.screen_name}
                    description={user.description}/>
              )}
          </ul>
      </div>
  );
};

UsersList.propTypes = {
  users: PropTypes.array.isRequired,
};

export default UsersList;
