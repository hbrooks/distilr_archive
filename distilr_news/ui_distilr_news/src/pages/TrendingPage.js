import React, { Component} from 'react'

import { getTrending } from "../backendProxy/wordTimelines";
import { renderSingleConcept } from '../components/TextTimeline'
import Loading from '../components/Loading'
import Uhoh from '../components/Uhoh'


class TrendingPage extends Component {

  constructor() {
    super()
    this.state = {
      trendingBackendResponse: null,
    };
    this.getAndSetTrending()
  }

  async getAndSetTrending() {
    const response = await getTrending();
    this.setState({
      trendingBackendResponse: response
    })
  }

  renderSingleMainBlockEntry(type, concepts) {
    console.log(type)
    console.log(concepts)
    return (
      <div
          style={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-around",
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              width: "25%",
              marginRight: "50px",
            }}
          >
            <h1>{type}</h1>
          </div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              flexDirection: "column",
              width: "75%",
            }}
          >
            {concepts.map(c => renderSingleConcept(c))}
          </div>
      </div>)

  }

  renderMainBlock(trendingBackendResponse) {
    let mainBlockContents = null;
    if (trendingBackendResponse === null) {
      mainBlockContents = (<Loading/>)
    } else if (trendingBackendResponse.statusCode === 406) {
      mainBlockContents = (<Uhoh/>)
    } else {
      const entries = Object.keys(trendingBackendResponse).map(k => this.renderSingleMainBlockEntry(k, trendingBackendResponse[k]))
      mainBlockContents = (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            flexDirection: "column",
            alignContent: "space-around",
          }} // TECH DEBT ALERT: this is how the timeline page is done, nested single divs like this.
        >
            <div
            style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-around",
                width: "70%",
              }}
          >
            {entries}
          </div>
        </div>)
    }
    return mainBlockContents;
  }

  render() {
    const trendingBackendResponse = this.state.trendingBackendResponse;
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          alignContent: "space-around",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            display: "flex",
            textAlign: "center",
            width: "55%",
            flexDirection: "row",
            alignContent: "space-around",
          }}
        >
          <h1 id="textLogo">
            distilr
          </h1>
          <h5
            style={{
              fontSize: '36px',
            }}
          >
            trending
          </h5>
        </div>
        {this.renderMainBlock(trendingBackendResponse)}
      </div>
    )
  }
}

export default TrendingPage