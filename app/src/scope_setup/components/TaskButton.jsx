import _ from 'lodash'
import React from 'react'
import PropTypes from 'prop-types'

import ButtonTasks from '../../common/tasks_buttons/components/ButtonTasks.jsx'

import { requestCreateTask } from '../../redux/tasks/actions.js'


class TaskButton extends React.Component {

	constructor(props) {
		super(props);

		this.runAmass = this.runAmass.bind(this);
	}

	shouldComponentUpdate(nextProps) {
		return !_.isEqual(nextProps, this.props);
	}

	runAmass(params) {
		this.context.store.dispatch(requestCreateTask(
			'amass',
			null,
			{'program': params},
			this.props.project_uuid
		));
	}

	render() {
		return (
			<ButtonTasks
				project_uuid={this.props.project_uuid}
				tasks={
				[
					{
						"name": "Amass",
                        "handler": this.runAmass,
						"help": [
							{
								"type": "info",
								"condition": true,
								"text": "Please use a separate field to specify the targets. Don't define -d parameter as it will create confusion"
							}
						],
						"preformed_options": [
							{
								"name": "Brute",
								"options": {
									"argv": "-brute -min-for-recursive 2"
								}
							},
							{
								"name": "Passive",
								"options": {
									"argv": "-passive"
								}
							},
							{
								"name": "With IPs",
								"options": {
									"argv": "-ip"
								}
							}
						],
						"available_options": [
							{
								"name": "hosts",
								"type": "text",
								"default_value": ""
							},
							{
								"name": "argv",
								"type": "text",
								"default_value": ""
							},
							{
								"name": "all_top_level_domains",
								"type": "checkbox",
								"default_value": false
							},
						]
					}
				]
				} />
		)
	}

}


TaskButton.contextTypes = {
    store: PropTypes.object
}

export default TaskButton;
