import axios, { AxiosInstance } from 'axios'

export interface SuiteCRMContact {
  id?: string
  email1: string
  first_name?: string
  last_name?: string
  lead_source?: string
  description?: string
}

export class SuiteCRMService {
  private client: AxiosInstance
  private sessionId: string | null = null

  constructor() {
    this.client = axios.create({
      baseURL: process.env.SUITECRM_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  async authenticate(): Promise<void> {
    try {
      const response = await this.client.post('/service/v4_1/rest.php', {
        method: 'login',
        input_type: 'JSON',
        response_type: 'JSON',
        rest_data: JSON.stringify({
          user_auth: {
            user_name: process.env.SUITECRM_USERNAME,
            password: process.env.SUITECRM_PASSWORD
          },
          application_name: 'AIC Newsletter Integration'
        })
      })

      if (response.data.id) {
        this.sessionId = response.data.id
      } else {
        throw new Error('Authentication failed: ' + JSON.stringify(response.data))
      }
    } catch (error) {
      console.error('SuiteCRM authentication error:', error)
      throw new Error('Failed to authenticate with SuiteCRM')
    }
  }

  async createContact(contact: SuiteCRMContact): Promise<string> {
    if (!this.sessionId) {
      await this.authenticate()
    }

    try {
      const response = await this.client.post('/service/v4_1/rest.php', {
        method: 'set_entry',
        input_type: 'JSON',
        response_type: 'JSON',
        rest_data: JSON.stringify({
          session: this.sessionId,
          module_name: 'Contacts',
          name_value_list: [
            { name: 'email1', value: contact.email1 },
            { name: 'first_name', value: contact.first_name || '' },
            { name: 'last_name', value: contact.last_name || 'Newsletter Subscriber' },
            { name: 'lead_source', value: contact.lead_source || 'Website Newsletter' },
            { name: 'description', value: contact.description || 'Newsletter subscription from AIC website' }
          ]
        })
      })

      if (response.data.id) {
        return response.data.id
      } else {
        throw new Error('Failed to create contact: ' + JSON.stringify(response.data))
      }
    } catch (error) {
      console.error('SuiteCRM create contact error:', error)
      throw new Error('Failed to create contact in SuiteCRM')
    }
  }

  async findContactByEmail(email: string): Promise<SuiteCRMContact | null> {
    if (!this.sessionId) {
      await this.authenticate()
    }

    try {
      const response = await this.client.post('/service/v4_1/rest.php', {
        method: 'get_entry_list',
        input_type: 'JSON',
        response_type: 'JSON',
        rest_data: JSON.stringify({
          session: this.sessionId,
          module_name: 'Contacts',
          query: `contacts.email1 = '${email}'`,
          order_by: '',
          offset: 0,
          select_fields: ['id', 'email1', 'first_name', 'last_name'],
          max_results: 1
        })
      })

      if (response.data.entry_list && response.data.entry_list.length > 0) {
        const entry = response.data.entry_list[0]
        return {
          id: entry.id,
          email1: entry.name_value_list.email1?.value || email,
          first_name: entry.name_value_list.first_name?.value,
          last_name: entry.name_value_list.last_name?.value
        }
      }

      return null
    } catch (error) {
      console.error('SuiteCRM find contact error:', error)
      throw new Error('Failed to search for contact in SuiteCRM')
    }
  }

  async updateContact(id: string, contact: Partial<SuiteCRMContact>): Promise<void> {
    if (!this.sessionId) {
      await this.authenticate()
    }

    try {
      const nameValueList = Object.entries(contact)
        .filter(([_, value]) => value !== undefined)
        .map(([name, value]) => ({ name, value: String(value) }))

      nameValueList.push({ name: 'id', value: id })

      await this.client.post('/service/v4_1/rest.php', {
        method: 'set_entry',
        input_type: 'JSON',
        response_type: 'JSON',
        rest_data: JSON.stringify({
          session: this.sessionId,
          module_name: 'Contacts',
          name_value_list: nameValueList
        })
      })
    } catch (error) {
      console.error('SuiteCRM update contact error:', error)
      throw new Error('Failed to update contact in SuiteCRM')
    }
  }
}

export const suiteCRM = new SuiteCRMService()
