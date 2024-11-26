import { Component, input } from '@angular/core';
import { assessmentStyles } from '../../constants';
import { SsvcEvaluationResult } from '../../types';
import { DecisionPointResultCardComponent } from '../decision-point-result-card/decision-point-result-card.component';
import { staggeredFadeIn } from '../../animations';

@Component({
    selector: 'app-ssvc-result-grid',
    templateUrl: 'ssvc-result-grid.component.html',
    standalone: true,
    imports: [DecisionPointResultCardComponent],
    animations: [staggeredFadeIn],
    styles: `
        :host {
            display: block;
        }
    `,
})
export class SsvcResultGridComponent {
    public readonly result = input.required<SsvcEvaluationResult>();

    protected readonly assessmentStyles = assessmentStyles;
}
