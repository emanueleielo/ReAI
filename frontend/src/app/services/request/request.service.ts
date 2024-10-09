import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class RequestService {

  endpoint = 'http://localhost/api/';

  constructor(private http: HttpClient) { }

  post(path: string, body: any){
    const formData = new FormData();
    for (const key of Object.keys(body)) {
      formData.append(key, body[key]);
    }
    return this.http.post(this.endpoint + path, formData)
  }

  postWithStream(path: string, body: any) {

    const formData = new FormData();
    for (const key of Object.keys(body)) {
      formData.append(key, body[key]);
    }

    return this.http.post(this.endpoint + path, formData, {
      observe: 'response',
      responseType: 'text'
    });
  }

  get(path: string, bodyEncoded?: any): Observable<any>{
    path = this.getBodyEncoded(path, bodyEncoded);
    return this.http.get(this.endpoint + path)
  }

  getBodyEncoded(path: string, bodyEncoded: any) {
    let index = 0;
    if (bodyEncoded) {
      Object.entries(bodyEncoded).forEach((value) => {
        if (value[1] !== undefined && value[1] !== null && value[1] !== '' && value[1] !== 'undefined') {
          path = path + ((index === 0) ? '?' : '&') + value[0] + '=' + encodeURIComponent(String(value[1]));
          index += 1;
        }
      })
    }
    return path;
  }

  downloadFile(url: string, folderToZip: string): Observable<{ filename: string; data: Blob }> {
    // Imposta i parametri per il corpo della richiesta
    const body = new HttpParams().set('folder_to_zip', folderToZip);

    return this.http.post(this.endpoint + url, body.toString(), {
      headers: new HttpHeaders({
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      }),
      observe: 'response',
      responseType: 'blob'
    }).pipe(
      map((response: any) => {
        // Estrai il nome del file dall'intestazione Content-Disposition
        const contentDisposition = response.headers.get('Content-Disposition') || '';
        const matches = /filename="(.+)"/.exec(contentDisposition);
        const filename = (matches && matches[1]) ? matches[1] : 'untitled';

        return {
          filename: filename,
          data: response.body as Blob
        };
      })
    );
  }

}

