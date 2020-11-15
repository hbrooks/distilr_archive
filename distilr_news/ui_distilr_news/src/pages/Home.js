import React, { Component} from 'react'
import { Redirect } from 'react-router'
import {
  Link
} from "react-router-dom";
import { encodeUrlString } from '../backendProxy/utilities';
// import NavigationFooter from './NavigationFooter'

class SearchSection extends Component {

  constructor () {
    super();
    this.state = {
      value: '', // The current text being searched for.
      shouldRedirectTo: '',
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSearchButtonClick = this.handleSearchButtonClick.bind(this);
    this.handleTrendingButtonClick = this.handleTrendingButtonClick.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  async handleSearchButtonClick(event) {
    event.preventDefault();  // TODO: Don't know what this line does.
    if (this.state.value !== '') {
      this.setState({
        shouldRedirectTo: "search",
      })
    }
  }

  async handleTrendingButtonClick(event) {
    event.preventDefault();  // TODO: Don't know what this line does.
    this.setState({
      shouldRedirectTo: "trending",
    })
  }

  render() {
    if (this.state.shouldRedirectTo === "search") {
      return (
        <Redirect
          push
          to={{
            pathname: '/timelines/search',
            search: `?q=${encodeUrlString(this.state.value)}`,
          }}
        />
      )
    } else {
      return (<div
        style={{
          display:  'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexDirection: "column",
      }}>
        <input 
          type="text"
          placeholder="Type a topic to learn about..."
          value={this.state.value}
          onChange={this.handleChange} 
          outline="none"
          style={{
            display: 'flex',
            width: "400px",
            height: "24px",
            justifyContent: 'center',
            marginBottom: '20px',
            padding: "3px 6px",
          }}
          autoFocus
        >
        </input>
        <div style={{
          display:  'flex',
          flexDirection: "row",
          justifyContent: 'center',
        }}>
          <Link
            className="button medium" 
            to="/trending"
            // onClick={this.handleTrendingButtonClick}
            style={{
              display: 'flex',
              flexDirection: "row",
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            trending
          </Link>

          <div
            className="button medium" 
            onClick={this.handleSearchButtonClick}
            style={{
              display:  'flex',
              flexDirection: "row",
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            go
          </div>
        </div>
      </div>)
    }
  }
}

// Rename to HomePage
class Home extends Component {
  render() {
    return (
      <div
        className="flexColumn"
        style={{
          height: "62vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
        }}
      >
        <h1 id="textLogo">
          distilr
        </h1>
        <h2 id="textSubLogo">
          News.  Research.  Conversation.
        </h2>

        <SearchSection/>

        <p id="homeExplanationText" style={{
            marginTop:"100px",
            width: '80%',
            position:'absolute',
            bottom:10,
            height: 50,
        }}>
Distilr News brings you novel insight into the social perspective on current events.  See what you can <a href='http://localhost:7000/'>learn here</a>.
        </p>
        
        {/* <NavigationFooter/> */}

      </div>
    )
  }
}

export default Home