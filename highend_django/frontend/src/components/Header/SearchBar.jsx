import React, { Component } from "react";
import {
  Link,
  withRouter
} from "react-router-dom";
import '../../css/search-bar.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { connect } from "react-redux";
import { fetchProducts } from '../../js/actions/index';



function mapStateToProps(state) {
  return { products: state.products };
}  

function mapDispatchToProps(dispatch) {
  return {
    fetchProducts: (brandName, pageNum, searchQuery) => dispatch(fetchProducts(brandName, pageNum, searchQuery)),
  };
}


class SearchBar extends Component {
  constructor(props){
  	super(props);
  	this.state = {
  		inputText: ''
  	};
  	this.handleInputSubmit = this.handleInputSubmit.bind(this);
  }

  componentDidUpdate(){
  	console.log(this.state.inputText);
  }

  handleInputTextChange(event){
  	this.setState({
  		inputText: event.target.value
  	});
  }

  handleInputSubmit(){
  	this.props.fetchProducts(null, null, this.state.inputText);
    this.props.history.push(`/products`);
  }

  handleKeyPress(target){
  	console.log("Hello??", this.state.inputText);
    if(target.charCode==13){
      this.handleInputSubmit();
    }
  }
  
  render(){
  	let inputBoxClass = "";
  	let containerClass = "";
  	if (this.props.searchbarLocation == "frontpage"){
  		containerClass = "frontpage-searchbar-container";
  		inputBoxClass = "frontpage-searchbar";
  	}else{
  		containerClass = "header-searchbar-container";
  		inputBoxClass = "header-searchbar";
  	}
    return(
      <div id="searchBarContainer" className={containerClass}>
      	<FontAwesomeIcon className="search-icon" icon={faSearch} />
        <input id="searchBar" type="text" name="fname"
        	className={inputBoxClass}
        	onChange={(e) => {this.handleInputTextChange(e)}}
        	onKeyPress={e => this.handleKeyPress(e)}
        	value={this.state.inputText}
        	onSubmit={this.handleInputSubmit}
        />
      </div>
    );
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(SearchBar));