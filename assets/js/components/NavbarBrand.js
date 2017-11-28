import React from 'react';
import PropTypes from 'prop-types';

import { Urls } from 'utils';


const NavbarBrand = ({ title, url }) => {
  return (
        <a className="navbar-brand" href={url}>{title}</a>
  );
};

NavbarBrand.propTypes = {
  title: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
};

export default NavbarBrand;
