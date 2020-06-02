import React, { Component } from "react";
import { render } from "react-dom";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    console.log("!!!");
    console.log(this.state.data);

    fetch("api/brands")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data: [data],
            loaded: true
          };
        });
      });
  }

  render() {
    console.log("!!!");
    console.log(this.state.data);
    if(this.state.data && this.state.data[0]) {
      return (

        <ul>
          {this.state.data[0]['results'].map(contact => {
            return (
              <li key={contact.unique_id}>
                {contact.name}
              </li>
            );
          })}
        </ul>
      );
    } else {
      return (<div></div>);
    }
    
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);