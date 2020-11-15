import React, { Component } from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";


import './Style.css'
import Home from './pages/Home'
import TimelinePage from './pages/TimelinePage'
import TrendingPage from './pages/TrendingPage';


class App extends Component {
  constructor() {
    super();
    this.state = {
      name: 'React'
    };
  }
  render() {
    return (
      // <Router>
      //   <Switch>
      //     <Route 
      //       path="/timelines"
      //       render={(props) => <TimelinePage {...props}/>}/>
      //     <Route 
      //       path="/"
      //       component={Home}
      //     />
      //      {/* <Route 
      //       path="/trending"
      //       render={TrendingPage}/> */}
      //   </Switch> 
      // </Router>
      <Router>
        <Switch>

          <Route path="/trending">
            <TrendingPage />
          </Route>

          <Route 
            path="/timelines"
            render={(props) => <TimelinePage {...props}/>}/>

          <Route path="/">
            <Home />
          </Route>

        </Switch>
    </Router>
    );
  }
}
  

export default App