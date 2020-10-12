import axios from 'axios';
import { FETCH_PRODUCTS, CHANGE_NAVIGATION_CATEGORY, EXIT_NAVIGATION_MENU } from "../constants/action-types";
import { trackPromise } from 'react-promise-tracker';

export function fetchProducts(brandName, pageNum, searchQuery) {
	console.log("gets to fetch products");

	let url = '/api/products/?';
	console.log("HERE's BRANDNAME: ", brandName);
	if (brandName) {
		url += `brandName=${encodeURI(brandName)}&`;
	} 
	if (pageNum) {
		url += `page=${pageNum}&`;
	} else {
		url += `page=1&`;
	}
	if (searchQuery) {
		url += `searchQuery=${encodeURI(searchQuery)}`;
	}

	return (dispatch) => {
		// dispatch({ type: START_FETCHING_BRAND_PRODUCTS });
		trackPromise(fetch(url)
		.then(response => response.json())
		.then(json => {
			console.log(json);
			dispatch({
				type: FETCH_PRODUCTS,
				payload: json,
			});
		}));
	}
}

export function changeNavigationCategory(category) {
	console.log("hello change navi", category);
	return { type: CHANGE_NAVIGATION_CATEGORY, payload: category };
}

export function exitNavigationMenu() {
	return { type: EXIT_NAVIGATION_MENU };
}
