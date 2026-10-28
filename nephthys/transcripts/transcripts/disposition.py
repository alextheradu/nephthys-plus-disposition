from pydantic import model_validator

from nephthys.transcripts.transcript import Transcript


class Disposition(Transcript):
    """Benjamin's messages for Disposition. Channels and FAQ come from env vars."""

    program_name: str = "Disposition"
    faq_link: str = ""
    faq_canvas_id: str | None = None
    faq_events_question: str | None = None

    ticket_reopen: str = "This Disposition support ticket was reopened by <@{helper_slack_id}>. Someone from the team will follow up soon."
    thread_broadcast_delete: str = "Please keep your messages in one thread so the Disposition team can follow along. I removed that message from the channel."
    ticket_feedback_text: str = "Thanks for helping us improve Disposition support!"
    stale_tickets_macro: str = "Hey (user), this Disposition support ticket has been inactive, so I'm closing it. Please start a new thread if you still need help."

    @model_validator(mode="after")
    def set_default_messages(self):
        # Build these after config is loaded so links use production channel IDs.
        faq_reminder = (
            f"\nWhile you wait, check <{self.faq_link}|the Disposition FAQ> for answers to common questions."
            if self.faq_link
            else ""
        )
        if not self.first_ticket_create:
            self.first_ticket_create = (
                "Hey (user), welcome to Disposition! I'm Benjamin, here to help the team keep track of your question. "
                "Someone from the Disposition team will be with you soon."
                f"{faq_reminder}\nOnce your question is answered, please mark this thread as resolved using the button below."
            )
        if not self.ticket_create:
            self.ticket_create = (
                "Hey (user), Benjamin here! Your Disposition support ticket is in the queue. "
                "Someone from the team will help you soon."
                f"{faq_reminder}\nPlease keep any extra details in this thread, and mark it as resolved once you're all set."
            )
        if not self.ticket_resolve:
            self.ticket_resolve = (
                "This Disposition support ticket was marked as resolved by <@{user_id}>. "
                f"If you need more help, start a new thread in <#{self.help_channel}>."
            )
        if not self.ticket_resolve_stale:
            self.ticket_resolve_stale = (
                "This Disposition support ticket has been inactive, so it was closed. "
                f"If you still need help, start a new thread in <#{self.help_channel}>."
            )
        if not self.faq_macro:
            self.faq_macro = (
                f"Hey (user), take a look at <{self.faq_link}|the Disposition FAQ> for help with this question. "
                "Please start a new thread if you still need help."
                if self.faq_link
                else f"Hey (user), please check the pinned resources in <#{self.help_channel}>. "
                "Please start a new thread if you still need help."
            )
        if not self.identity_macro:
            self.identity_macro = f"Hey (user), please ask identity verification questions in <#{self.identity_help_channel}> so the verification team can help."
        if not self.not_allowed_channel:
            self.not_allowed_channel = f"Please ask <@{self.program_owner}> if you need access to this Disposition support channel."
        return self
