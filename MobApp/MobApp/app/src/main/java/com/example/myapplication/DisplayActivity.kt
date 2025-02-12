package com.example.myapplication

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.FragmentManager

class DisplayActivity : AppCompatActivity(),
    BlackFrag.OnSeekBarChangeListener,
    WhiteFrag.OnDateChangeListener {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_display)

        val fragmentManager: FragmentManager = supportFragmentManager

        // Устанавливаем BlackFrag по умолчанию
        fragmentManager.beginTransaction()
            .replace(R.id.frame, BlackFrag.newInstance())
            .commit()

        findViewById<Button>(R.id.frag1button).setOnClickListener {
            fragmentManager.beginTransaction()
                .replace(R.id.frame, BlackFrag.newInstance())
                .commit()
        }

        findViewById<Button>(R.id.frag2button).setOnClickListener {
            fragmentManager.beginTransaction()
                .replace(R.id.frame, WhiteFrag.newInstance())
                .commit()
        }
    }

    // Обработка события от BlackFrag
    override fun onSeekBarPositionChanged(position: Int) {
        val displayTextView = findViewById<TextView>(R.id.display_view)
        displayTextView.text = "SeekBar Position: $position"
    }

    // Обработка события от WhiteFrag
    override fun onDateSelected(date: String) {
        val displayTextView = findViewById<TextView>(R.id.display_view)
        displayTextView.text = "Selected Date: $date"
    }
}