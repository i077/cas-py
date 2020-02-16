import React from 'react';
import { HistoryElement } from "./HistoryElement";
import { HistoryScroll } from "./HistoryScroll";
import './History.css';

export class History extends React.Component {
    constructor(props) {
        super(props);

        this.handleElement = this.handleElement.bind(this);
    }

    handleElement(clickValue) {
        this.props.handleHistory(clickValue);
    }

    render() {

        const historyList = this.props.history.map((historyItem, index) =>
            <HistoryElement key={index} historyItem={historyItem} handleClick={this.handleElement} />
        );
        return (
            <div className="history-div">
                <p>History:</p>
                <div className="history-list-div">
                    {historyList}
                    <HistoryScroll />
                </div>
            </div>
        );
    }
}
