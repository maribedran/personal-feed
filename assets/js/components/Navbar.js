import React from 'react';
import PropTypes from 'prop-types';

import { Urls } from 'utils';


const Navbar = ({ title }) => {
	const homeURL = Urls.home();

	return (
  		<nav className="navbar navbar-inverse bg-inverse">
  			<div className="container">
  				<a className="navbar-brand" href={homeURL}>{title}</a>
  			</div>
		</nav>
	);
};

Navbar.propTypes = {
	title: PropTypes.string.isRequired,
};

export default Navbar;
