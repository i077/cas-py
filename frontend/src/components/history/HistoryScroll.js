import React from 'react';

export class HistoryScroll extends React.Component {
    componentDidMount() {
        this.scrollToBottom();
    }

    componentDidUpdate() {
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.el.scrollIntoView({ behavior: 'smooth' });
    }

    render() {
        return <div ref={el => { this.el = el; }} />
    }
}
