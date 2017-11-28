import React from 'react';
import PropTypes from 'prop-types';

import { Urls } from 'utils';

import NavbarBrand from 'components/NavbarBrand'


const Navbar = ({ title }) => {
  const homeURL = Urls.home();

  return (
      <nav className="navbar">
        <NavbarBrand url={homeURL} title={title} />
      </nav>
  );
};

Navbar.propTypes = {
  title: PropTypes.string.isRequired,
};

export default Navbar;
