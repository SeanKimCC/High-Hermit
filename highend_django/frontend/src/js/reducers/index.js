import { FETCH_BRAND_PRODUCTS, CHANGE_NAVIGATION_CATEGORY ,EXIT_NAVIGATION_MENU} from "../constants/action-types";

const initialState = {
  products: [],
  navigationCategory: null,
  showNavigationMenu: false,
};

function rootReducer(state = initialState, action) {
	if(action.type === FETCH_BRAND_PRODUCTS) {
		return {...state, products: action.payload};
	} else if(action.type === CHANGE_NAVIGATION_CATEGORY) {
		console.log("13", action.payload);
		return {...state, navigationCategory: action.payload, showNavigationMenu: true};
	} else if(action.type === EXIT_NAVIGATION_MENU) {
		return {...state, showNavigationMenu: false};
	}
	return state;
}

export default rootReducer;