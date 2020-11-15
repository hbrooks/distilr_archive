import React, { Component } from 'react'

import Loading from '../components/Loading'
import Uhoh from '../components/Uhoh'
import { TextTimeline } from '../components/TextTimeline'
import { createTimeline } from '../backendProxy/wordTimelines'


class TimelinePage extends Component {

  constructor (props) {
    super(props)
    const queryStringLibrary = require('query-string');
    const queryParams = queryStringLibrary.parse(this.props.location.search);
    this.state = {
      backendResponse: null,
    };
    this.search(queryParams.q)
  }

  async search(queryString) {
    const response = await createTimeline(queryString)
    this.setState({
      backendResponse: response,
    })
  }

  render() {
    const { 
      backendResponse,
    } = this.state;

    if (backendResponse === null) {
      return (
        <Loading/>
      )
    } else if (backendResponse.statusCode === 406) {
      return (<Uhoh/>)
    } else {
      const timelineProps = {
        timeStart: backendResponse.timeStart,
        timeEnd: backendResponse.timeEnd,
        dateToData: backendResponse.content,
        topicConcept: backendResponse.topicConcept,
      }
      return (
        <TextTimeline {...timelineProps}/>
      )
    }
  
  }
  
}

export default TimelinePage