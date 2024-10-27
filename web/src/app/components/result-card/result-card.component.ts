import { Component, input } from '@angular/core';
import { NgClass } from '@angular/common';
import { EvaluationResult } from '../../types';
import { assessmentStyles } from '../../constants';

@Component({
    selector: 'app-result-card',
    templateUrl: 'result-card.component.html',
    standalone: true,
    imports: [NgClass],
})
export class ResultCardComponent<T> {
    public readonly title = input.required<string>();
    public readonly category = input.required<string>();
    public readonly result = input.required<EvaluationResult<T>>();

    protected get badgeClass(): string {
        const assessment = this.result().assessment as string;
        return assessmentStyles[this.category()][assessment];
    }

    protected formatAssessment(value: string): string {
        return value
            .replace(/_/g, ' ')
            .replace(/\b\w/g, char => char.toUpperCase());
    }
}
