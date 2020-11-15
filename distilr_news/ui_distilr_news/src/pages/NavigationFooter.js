import React, { Component} from 'react'
import { BrowserRouter as Router, Link } from 'react-router-dom';

import '../Style.css'


class NavigationFooter extends Component {
  
  render() {
    const noUnderlineStyle = {'textDecoration': 'none'};

    const footerButtons = [
      {
        to: "/",
        text: "Home"
      },
      // TODO: Add more!
    ]

    const footerComponents = []
    footerButtons.forEach((element, index) => {
      footerComponents.push((
        <div 
          key={index}
          style={{
            display: 'flex',
            width: "90px",
            height: "20px",
            justifyContent: 'center',
        }}>
          <Link
            to={element.to}
            style={noUnderlineStyle}
          >
            {element.text}
          </Link>
        </div>
      ))
    })

    return (
      <div
        style={{
          display:  'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          position: "absolute",
          bottom: 0,
          width: "25%",
          height: "75px",
      }}>
        <Router>
          {footerComponents}
        </Router>
      </div>
    )}
}

export default NavigationFooter