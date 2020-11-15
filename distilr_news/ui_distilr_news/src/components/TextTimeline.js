import React, { Component } from 'react'


const renderSingleConcept = (c => {
  return (
    <a 
      style={{
        fontSize: "18px",
        textAlign: "right",
      }}
      href={`http://localhost:7000/timelines/search?q=${c.label}`} // TODO: Add id as a query param.
    >
      {c.label}
    </a>
  )
})


class TextTimeline extends Component {

  constructor(props) {
    super(props)
  }

  renderSingleEvent(e) {
    return (
      <div> 
        <h4
          style={{
            fontSize: "20px",
          }}
        >
          {e.title}
        </h4>
        <p>{e.summary}</p>
      </div>
    )
        
  }

  renderSingleLineItem(date, dataForDate) {
    const publishedAt = new Date(date * 1000);
    const allEvents = dataForDate.events.map(e => this.renderSingleEvent(e))
    const allConcepts = dataForDate.concepts.map(c => renderSingleConcept(c))

    return (
      <div>
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
                  flexDirection: "column",
                  width: "25%",
                  marginRight: "50px",
                }}
              >
              <h3
                style={{
                  textAlign: "right",
                  fontSize: "28px",
                }}
              >
                {publishedAt.toLocaleDateString(undefined, {weekday: "long", day: "numeric", month: "long"})}
              </h3>
              {allConcepts}
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-around",
                width: "75%",
              }}
            >
              {allEvents}
            </div>
          </div>
      </div>
    )
  }

  renderAll(dateToData) {
    const lineItems = Object.keys(dateToData).map(key => this.renderSingleLineItem(key, dateToData[key]))
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-around",
          width: "70%",
        }}
      >
        {lineItems}
      </div>
    )
  }

  renderTypeText(typeText) {
    // if (typeText !== undefined) {
    //   return (<p> ({typeText}) </p>);
    // }
  }
  
  render() {
    const uri = this.props.topicConcept.uri
    const label = this.props.topicConcept.label
    const type = this.props.topicConcept.type
    
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
          alignContent: "space-around",
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
          <h1 
            style={{
              fontSize: "38px",
            }}
            href={uri}
          >
            {label}
          </h1>
          <p>
            {this.renderTypeText(type)}
          </p>
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            flexDirection: "column",
            alignContent: "space-around",
          }}
        >
        {this.renderAll(this.props.dateToData)}
      </div>
    </div>

    )
  }
}


export {
  TextTimeline,
  renderSingleConcept
};