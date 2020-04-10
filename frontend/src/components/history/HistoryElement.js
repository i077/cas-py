import React from 'react';
import TeX from '@matejmazur/react-katex';
import './HistoryElement.css';
import { KatexSettings } from "../KatexSettings";

const assign_string = ':=';

export class HistoryElement extends React.Component {
    constructor(props) {
        super(props);

        this.elementClick = this.elementClick.bind(this);
    }

    elementClick() {
        this.props.handleClick(this.props.historyItem);
    }

    getHistoryItemOutput() {
        const item = this.props.historyItem;
        if (item.input.includes(assign_string)) {
            return item.input;
        } else {
            return item.input + ' = ' + item.output;
        }
    }

    render() {
        return (
            <div className="history-item-div" onClick={this.elementClick}>
                <div className="history-item-id-div">
                    [{this.props.historyItem.id}]
                </div>
                <div className="history-item-text-div">
                    <TeX
                        math={this.getHistoryItemOutput()}
                        errorColor={'#cc0000'}
                        settings={KatexSettings}
                    />
                </div>
            </div>
        );
    }
}
