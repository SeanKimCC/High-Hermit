import React, { Component } from "react";
import { render } from "react-dom";
import '../css/header.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useParams
} from "react-router-dom";
import { connect } from 'react-redux';
import { changeNavigationCategory, exitNavigationMenu } from "../js/actions/index";

function mapDispatchToProps(dispatch) {
  return {
    changeNavigationCategory: category => dispatch(changeNavigationCategory(category)),
    exitNavigationMenu: () => dispatch(exitNavigationMenu()),
  };
}

function mapStateToProps(state) {
  return { showNavigation: state.showNavigationMenu, navigationCategory: state.navigationCategory };
}  

class HeaderNavigationMenu extends Component {
  constructor(props) {
    super(props);
    this.state = {
      toggleToUpdate: false
    };
  }

  ClothingMenu() {

  }

  DesignersMenu() {
    const brands = this.props.brandData[0]['results'].map(brand => {
      return (
        <li className="brand-menu-link">
          <Link to={`/products/${encodeURI(brand.name)}&pageNum=${1}`}>{brand.name}</Link>
        </li>
      );
    });
    return brands;

  }
  

  render() {
    const hello = this.props.category;
    console.log("21", this.props.category, this.props.showNavigation);
    return (
      this.props.showNavigation ? 
      <div id="naviMenu" className="header--navigation-menu borderbox">
        {this.props.category}
        {this.DesignersMenu()}
      </div>
      : <div></div>
    );
  }
}

class HeaderItem extends Component {

  constructor(props) {
    super(props);
    this.handleMouseHover = this.handleMouseHover.bind(this);
    this.state = {
      isHovering: false,
    };
  }

  handleMouseHover() {
    const category = this.props.category;
    console.log(category, this.props.category);
    this.props.changeNavigationCategory(this.props.category);
  }

  render() {
    return (
      <li className="header--navli borderbox" onMouseOver={this.handleMouseHover}>
        <div className="header--navitem borderbox">
          <a className="header--item-link borderbox">
            {this.props.category}
          </a>
        </div>
      </li>
    );
  }
}

class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      brandName: '',
      productData: [],
      loaded: false,
      placeholder: "Loading"
    };
    this.exitNavigationMenu = this.exitNavigationMenu.bind(this);
  }

  exitNavigationMenu() {
    console.log("exitting");
    this.props.exitNavigationMenu();
  }

  render() {
    return (
      <div className="header--container borderbox">
        <Link to="/"><div className="header--title borderbox" onMouseOver={this.props.exitNavigationMenu}>Ay Papi</div></Link>
        <div className="header--menu borderbox">
          <nav className="header--navbar borderbox">
            <ul className="header--navgroup borderbox">
              <HeaderItem 
                category="Clothing" 
                changeNavigationCategory={this.props.changeNavigationCategory}
              />
              <HeaderItem 
                category="Designers" 
                changeNavigationCategory={this.props.changeNavigationCategory}
              />
              <HeaderItem 
                category="Ipsum" 
                changeNavigationCategory={this.props.changeNavigationCategory}
              />
              <HeaderItem 
                category="Loren" 
                changeNavigationCategory={this.props.changeNavigationCategory}
              />
            </ul>
          </nav>

        </div>
        <HeaderNavigationMenu
          category={this.props.navigationCategory}
          showNavigation={this.props.showNavigation}
          brandData={this.props.brandData}
        /> 
      </div>);
    
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Header);