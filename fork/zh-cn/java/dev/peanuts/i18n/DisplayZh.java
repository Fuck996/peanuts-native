package dev.peanuts.i18n;

import android.widget.TextView;
import dev.nxnative.android.R;

/** Display-only adapter. The exact original text stays available to code that routes by a row title. */
public final class DisplayZh {
    private DisplayZh() {}
    public static void set(TextView view, CharSequence source) {
        view.setTag(R.id.peanuts_source_text, source);
        view.setText(L10n.tr(source));
    }
    public static CharSequence source(TextView view) {
        CharSequence shown = view.getText();
        Object raw = view.getTag(R.id.peanuts_source_text);
        if (raw instanceof CharSequence && android.text.TextUtils.equals(shown, L10n.tr((CharSequence) raw))) {
            return (CharSequence) raw;
        }
        return shown;
    }
    public static String sourceString(TextView view) {
        return String.valueOf(source(view)).trim();
    }
}
