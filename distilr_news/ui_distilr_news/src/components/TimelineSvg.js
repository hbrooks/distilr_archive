// import React, { Component } from 'react'
// import * as d3 from 'd3'


// const oneDayInSeconds = 60*60*24;
// const oneWeekInSeconds = 7*oneDayInSeconds;

// class Timeline extends Component {

//   constructor(props) {
//     super(props)
//     // NOTE: I believe this this.state.isTimelineShowing thing is to create a div with
//     // the ID then add to it.  Maybe it should be renamed to "drawingComplete"
//     this.state = {
//       isTimelineShowing: false
//     }
//   }

//   componentDidMount() {
//     if (!this.state.isTimelineShowing) {
//       this.drawAxis();
//     }
//   }

//   componentWillUnmount() {
//     this.setState({
//       isTimelineShowing: false,
//     })
//   }

//   drawAxis() {
//     const {
//       timeStart,
//       timeEnd,
//       content,
//     } = this.props;

//     const window = {
//       innerWidth: 800,
//       innerHeight: 800
//     }

//     // Ratios of window size.
//     const margin = {
//       top: .10,
//       bottom: .10,
//       right: 0.25,
//       left: 0.25
//     }

//     const timelineWidth = window.innerWidth*(1 - margin.left - margin.right) 
//     const timelineHeight = window.innerHeight*(1 - margin.top - margin.bottom);

//     var svg = d3
//       .select("#timelineContainer") // Selects a div where id=timelineContainer.
//       .append("svg")
//       .attr("width", timelineWidth)
//       .style("transform", "translate(50%, 0)") // Center axis in container.
//       .attr("height", timelineHeight)

//     const borderFraction = 0.10;

//     const timelineTimeSpanInPosix = Math.max(
//       timeEnd - timeStart,
//       4*oneWeekInSeconds
//     );

//     const timelineDomainMin = timeStart - borderFraction*timelineTimeSpanInPosix
//     const timelineDomainMax = timeEnd + borderFraction*timelineTimeSpanInPosix

//     const timelineScale = d3.scaleTime()
//         .domain([timelineDomainMin, timelineDomainMax])
//         .range([0, timelineHeight])

//     const timelineAxis = d3.axisLeft(timelineScale)
//         .ticks(0) // No ticks.

//     svg.append("g")
//         .attr("class", "axis") // Define a <g class="axis"> in the SVG.
//         .call(timelineAxis)
//         .style("transform", "translate(50%, 0)"); // Center axis in SVG.

//     var tokenLeftOrRightCoeff = 1    

//     content.forEach(content => {

//       const {
//         publishedAt,
//         concepts,
//         summary,
//         title,
//         uri,
//         wgt,
//       } = content;
    
//       const location = {
//           x: (timelineWidth/2) + 15*tokenLeftOrRightCoeff,
//           y: timelineScale(publishedAt)
//       }

//       const contentElementLinkText = title
//       const contentElementLinkUrl = uri

//       const textAnchor = tokenLeftOrRightCoeff === 1 ? 'start' : 'end'

//       svg.append('text')
//           .attr("transform", `translate(${location.x}, ${location.y})`)
//           .attr("text-anchor", textAnchor)
//           .html(`<a href=${contentElementLinkUrl}>${contentElementLinkText}</a>`)

//       tokenLeftOrRightCoeff = -1*tokenLeftOrRightCoeff

//     })

//     this.setState({
//       isTimelineShowing: true,
//     })

//   }
  
//   render() {
//     return (
//     <div>
//       <h1>TODO</h1>
//       <div id="timelineContainer"/>
//     </div>
//     )
//   }
// }


// export default Timeline;