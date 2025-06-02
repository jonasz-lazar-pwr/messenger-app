import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-message-bubble',
  standalone: false,
  templateUrl: './message-bubble.component.html',
  styleUrl: './message-bubble.component.css'
})
export class MessageBubbleComponent {
  @Input() message: any;
  @Input() userSub!: string;
}
