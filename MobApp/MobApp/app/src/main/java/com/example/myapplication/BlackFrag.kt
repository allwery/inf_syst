package com.example.myapplication

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.SeekBar
import androidx.fragment.app.Fragment

class BlackFrag : Fragment() {
    private var listener: OnSeekBarChangeListener? = null

    interface OnSeekBarChangeListener {
        fun onSeekBarPositionChanged(position: Int)
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        if (context is OnSeekBarChangeListener) {
            listener = context
        } else {
            throw RuntimeException("$context must implement OnSeekBarChangeListener")
        }
    }

    override fun onDetach() {
        super.onDetach()
        listener = null
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_black, container, false)
        val seekBar = view.findViewById<SeekBar>(R.id.seekSlide)

        // Передача данных активности при изменении позиции
        seekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                listener?.onSeekBarPositionChanged(progress)
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })

        return view
    }

    companion object {
        @JvmStatic
        fun newInstance() = BlackFrag()
    }
}