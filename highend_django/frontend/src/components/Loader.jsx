import React, { Component } from "react";
import { usePromiseTracker, trackPromise } from "react-promise-tracker";
import Loader from 'react-loader-spinner';

const LoadingIndicator = props => {
  const { promiseInProgress } = usePromiseTracker();
  return (
    promiseInProgress && 
    <div id="loader"
      style={{
        position: "absolute",
        top: "0px",
        left: "0px",
        width: "100%",
        height: "100%",
        backgroundColor: "white",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Loader type="ThreeDots" color="#2BAD60" height="100" width="100" />
    </div>
  );  
}

export default LoadingIndicator;