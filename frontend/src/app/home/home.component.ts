import { Component } from '@angular/core';
import {RequestService} from "../services/request/request.service";
import {Configuration} from "../models/configuration/configuration";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  loading: boolean = false;
  loadingMessage: string = 'Loading...';
  step: number = 1;
  downloadFilePath: string = '';
  constructor(private requestService: RequestService) {
  }

  nextStep() {
    this.step++;
  }

  backStep() {
    this.step--;
  }

  restart() {
    this.step = 1;
  }

  startRefactoring(configuration: Configuration) {
    this.loading = true;
    this.nextStep();
    this.showLoadingMessages();
    this.requestService.postWithStream('process/', configuration).subscribe((res: any) => {
      this.downloadFilePath = this.extractLastNodeContent(res.body);
      this.loading = true;
    }, (error) => {
      this.loading = false;
      this.backStep();
      console.error('error', error);
    }, () => {
      this.loading = false;
      this.nextStep();
    });
  }

  // TODO: Right now the stream response not working, so we are using a delay to simulate the process
  private showLoadingMessages() {
    // Definisci i messaggi da visualizzare
    const messages = [
      'upload_files',
      'create_folder_structure',
      'read_files',
      'generate_requirements',
      'generate_technical_requirements',
      'generate_architecture_diagram',
      'generate_folder_file_structure',
      'generate_files',
      'start_application_and_test'
    ];

    // Funzione ricorsiva per mostrare i messaggi
    const displayMessage = (index: number) => {
      if (index < messages.length) {
        this.loadingMessage = messages[index];
        setTimeout(() => displayMessage(index + 1), 30000); // Aspetta 30 secondi prima di mostrare il prossimo messaggio
      }
    };

    displayMessage(0); // Inizia a mostrare i messaggi dal primo
  }

  extractLastNodeContent(input: string): string {
    const nodes = input.split('</node>');
    const node = nodes[nodes.length - 2];
    const node2 = node.split('|')
    return node2[node2.length - 1];

  }
}
